define('linkify-element', ['exports', 'module', './linkify'], function (exports, module, _linkify) {
	/**
 	Linkify a HTML DOM node
 */

	'use strict';

	var HTML_NODE = 1,
	    TXT_NODE = 3;

	/**
 	Given a parent element and child node that the parent contains, replaces
 	that child with the given array of new children
 */
	function replaceChildWithChildren(parent, oldChild, newChildren) {
		var lastNewChild = newChildren[newChildren.length - 1];
		parent.replaceChild(lastNewChild, oldChild);
		for (var i = newChildren.length - 2; i >= 0; i--) {
			parent.insertBefore(newChildren[i], lastNewChild);
			lastNewChild = newChildren[i];
		}
	}

	/**
 	Given an array of MultiTokens, return an array of Nodes that are either
 	(a) Plain Text nodes (node type 3)
 	(b) Anchor tag nodes (usually, unless tag name is overridden in the options)
 
 	Takes the same options as linkifyElement and an optional doc element
 	(this should be passed in by linkifyElement)
 */
	function tokensToNodes(tokens, opts, doc) {
		var result = [];

		for (var i = 0; i < tokens.length; i++) {
			var token = tokens[i];
			var validated = token.isLink && _linkify.options.resolve(opts.validate, token.toString(), token.type);

			if (token.isLink && validated) {

				var href = token.toHref(opts.defaultProtocol),
				    formatted = _linkify.options.resolve(opts.format, token.toString(), token.type),
				    formattedHref = _linkify.options.resolve(opts.formatHref, href, token.type),
				    attributesHash = _linkify.options.resolve(opts.attributes, href, token.type),
				    tagName = _linkify.options.resolve(opts.tagName, href, token.type),
				    linkClass = _linkify.options.resolve(opts.linkClass, href, token.type),
				    target = _linkify.options.resolve(opts.target, href, token.type),
				    events = _linkify.options.resolve(opts.events, href, token.type);

				// Build the link
				var link = doc.createElement(tagName);
				link.setAttribute('href', formattedHref);
				link.setAttribute('class', linkClass);
				if (target) {
					link.setAttribute('target', target);
				}

				// Build up additional attributes
				if (attributesHash) {
					for (var attr in attributesHash) {
						link.setAttribute(attr, attributesHash[attr]);
					}
				}

				if (events) {
					for (var event in events) {
						if (link.addEventListener) {
							link.addEventListener(event, events[event]);
						} else if (link.attachEvent) {
							link.attachEvent('on' + event, events[event]);
						}
					}
				}

				link.appendChild(doc.createTextNode(formatted));
				result.push(link);
			} else if (token.type === 'nl' && opts.nl2br) {
				result.push(doc.createElement('br'));
			} else {
				result.push(doc.createTextNode(token.toString()));
			}
		}

		return result;
	}

	// Requires document.createElement
	function linkifyElementHelper(element, opts, doc) {

		// Can the element be linkified?
		if (!element || typeof element !== 'object' || element.nodeType !== HTML_NODE) {
			throw new Error('Cannot linkify ' + element + ' - Invalid DOM Node type');
		}

		var ignoreTags = opts.ignoreTags;

		// Is this element already a link?
		if (element.tagName === 'A' || ignoreTags.indexOf(element.tagName) >= 0) {
			// No need to linkify
			return element;
		}

		var childElement = element.firstChild;

		while (childElement) {

			switch (childElement.nodeType) {
				case HTML_NODE:
					linkifyElementHelper(childElement, opts, doc);
					break;
				case TXT_NODE:

					var str = childElement.nodeValue,
					    tokens = _linkify.tokenize(str),
					    nodes = tokensToNodes(tokens, opts, doc);

					// Swap out the current child for the set of nodes
					replaceChildWithChildren(element, childElement, nodes);

					// so that the correct sibling is selected
					childElement = nodes[nodes.length - 1];

					break;
			}

			childElement = childElement.nextSibling;
		}

		return element;
	}

	function linkifyElement(element, opts) {
		var doc = arguments.length <= 2 || arguments[2] === undefined ? null : arguments[2];

		try {
			doc = doc || window && window.document || global && global.document;
		} catch (e) {/* do nothing for now */}

		if (!doc) {
			throw new Error('Cannot find document implementation. ' + 'If you are in a non-browser environment like Node.js, ' + 'pass the document implementation as the third argument to linkifyElement.');
		}

		opts = _linkify.options.normalize(opts);
		return linkifyElementHelper(element, opts, doc);
	}

	// Maintain reference to the recursive helper to cache option-normalization
	linkifyElement.helper = linkifyElementHelper;
	linkifyElement.normalize = _linkify.options.normalize;

	module.exports = linkifyElement;
});