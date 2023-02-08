import { mergeAttributes, Node } from '@tiptap/core';


export default Node.create({
	name: 'draggableItem',
	group: 'block',
	content: 'block+',
	draggable: true,

	parseHTML() {
		return [
			{
				tag: 'div[data-type="draggable-item"]',
			},
		]
	},

	renderHTML({HTMLAttributes}) {
		return ['div', mergeAttributes(HTMLAttributes, {'data-type': 'draggable-item'}), 0]
	},

	addNodeView() {
		return ({ editor, node, getPos, HTMLAttributes, decorations, extension }) => {
			//const dom = document.createElement('cms-component');
			const dom = document.createElement('div');
			dom.classList.add('draggable-item');

			const dragHandle = document.createElement('div');
			dragHandle.setAttribute('draggable', 'true');
			dragHandle.setAttribute('data-drag-handle', '');
			dragHandle.setAttribute('contenteditable', 'false');
			dragHandle.classList.add('drag-handle');
			dom.append(dragHandle);

			// dom.addEventListener('click', event => {
			// 	console.log('clicked on the container');
			// });

			const contentDOM = document.createElement('div')
			contentDOM.setAttribute('data-node-view-content', '')
			contentDOM.classList.add('content')
			dom.append(contentDOM);

			return {
				dom,
				contentDOM,
			}
		}
	},

});
