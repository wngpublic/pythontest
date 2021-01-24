

- npm 
  npm i
  npm i --production
  npm i -g
  npm i pkg
  npm i pkg@<version>
  npm i pkg --save    // add to package.json
  npm i pkg --save-dev  // add to package.json dev dependencies
  npm search [terms]
  npm update -g pkg
  npm update
  npm update -g
  npm update --dev
  npm remove -g pkg
  npm remove pkg
  npm uninstall [-g] pkg
  npm -v
  npm init
  npm list
  npm ls
  npm list -g
  npm view            // list latest version
  npm outdated
  npm i -g npm        // update npm
  npm run
  npm test
  npm cache clean

  npm i nodemon -g
  npm i nodemon --save-dev
  nodemon server.js port

- protobuf with node


- DOM notes
  getElementById, getElementsByName, getElementsByTagName, querySelector (for CSS), 
  document.querySelectorAll(s)
  get parentNode, childNodes, siblings, firstChild, previousSibling, nextSibling, lastChild
  createElement, appendChild, textContent, innerHHTML, append, prepend, replaceChild, removeChild
  createTextNode
  setAttribute, getAttribute, removeAttribute, hasAttribute
  mouse events, scroll events, focus events, keyboard events, load event, dispatchEvent
  
  - DocumentType, DocumentFragement, ChildNode, Element, Event, ParentNode, HTMLCollection,
    Node, NodeFilter, Range, Text, Window, Worker, URL, TreeWalker

  - get first link in document:
    document.body.getElementsByTagName("a")[0];
  - get all links in document
    document.body.getElementsByTagName("a")
