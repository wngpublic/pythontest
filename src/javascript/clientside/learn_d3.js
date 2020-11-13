

class DataType {
}

class TestDataNode {
    constructor(id,type,val,name,parent,children){
        this.id = id;
        this.type = type;
        this.val = val;
        this.name = name;
        this.parent = parent;
        this.children = children;
    }
}
class TestData {

    getTreeDataNodes1() {
        let id = 0;
        let type = null;
        let val = null;
        let name = null;
        let parent = null;
        let children = null;

        let r = new TestData(id,type,val,name,parent,children);
    }
}
class LearnD3 {
    constructor() {
        console.log('constructor called');
        this.fileinputText = null;
        this.svg = null;
        this.foo = null;
    }

    onloadReader(fileReader,cb) {
        const data = fileReader.result;
        this.fileinputText = data;
        document.getElementById('id-div-right-1').innerHTML = '<pre>' + this.fileinputText + '</pre>'; // json needs <pre>
        console.log(`readInputFile data onload`);
        //console.log(`readInputFile data onload ${data}`);
        // why is cb unable to access this.fileinputtext?? i have to use the this.renderDataAfterLoad. why???
        // you can, if you bind the callback before passing it!
        // let boundedThis = (this.renderDataAfterLoad).bind(this);

        cb();
        //this.renderDataAfterLoad(); // dont need to use this anymore because cb is bounded to this!
    }
    readInputFile(input,cb) {
        try {
            let filei = document.getElementById('file-selector-hierarchy').files[0];
            if(filei == null) {
                document.getElementById('id-div-left-txt').innerHTML = `no filename detected!`;
                return null;
            }
            let fileReader = new FileReader();
            fileReader.readAsText(filei);
            /*
            fileReader.onload = () => {
                // why is this keyword undefined? cannot set this.fileinputText 
                // dont use anonymous function to access this!
                this.fileinputText = fileReader.result; 
                inputData = fileReader.result;
                document.getElementById('id-div-right-1').innerHTML = '<pre>' + this.fileinputText + '</pre>'; // json needs <pre>
                console.log(`readInputFile data onload`);
            };
            */
            fileReader.onload = () => {
                // this is how to get the this reference. cannot use anonymous method!
                // so this.callback passed in is useless??
                this.onloadReader(fileReader,cb);
                //cb();
            }
            fileReader.onloadend = () => {
                console.log(`readInputFile onloadend`);
            }
            fileReader.onerror = () => {
                console.log(`error reading ${filei}`);
            }
            return true;
        } catch(e) {
            console.log(e);
            return null;
        }
    }
    
    updateHierarchyText(input) {
        console.log(`updateHierarchyText ${input}`);
    }

    renderDataAfterLoad() {
        console.log(`calling renderDataAfterLoad:`);
        const margin = {top: 200, right: 100, bottom: 20, left: 20},
        width  = 600 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;
  
        const treemap = d3.tree().size([height, width]);
        const jsonData = JSON.parse(this.fileinputText);

        const nodes = treemap(d3.hierarchy(jsonData, d => d.children));

        const svg = d3.select('body')
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .attr('transform','translate(' + margin.left + ',' + margin.top + ')');

        this.svg = svg;

        const link = svg.selectAll('.link')
            .data(nodes.descendants().slice(1))
            .enter()
            .append('path')
            .attr('class','link')
            .attr('stroke','lightgray')
            .attr('fill','none')
            .attr('d', d => {
                return 'M' + d.y + ',' + d.x
                + 'C' + (d.y + d.parent.y) / 2 + ',' + d.x
                + ' ' + (d.y + d.parent.y) / 2 + ',' + d.parent.x
                + ' ' + d.parent.y + ',' + d.parent.x;
            });
        
        const node = svg.selectAll('node')
            .data(nodes.descendants())
            .enter()
            .append('g')
            .attr('transform', d => 'translate(' + d.y + ',' + d.x + ')');
        
        node.append('circle')
            .attr('r', 3)
            .attr('fill','black');

        node.append('text')
            .attr('x', 0)
            .attr('y', 15)
            .attr('class','node')
            .attr('keytext', d => d.data.name)
            .attr('keyval', d => d.data.val)
            .text(d => `${d.data.name}:${d.data.val}`);

        let boundedThis = (this.clickSelect).bind(this);
        svg.selectAll('text')
            .attr('pointer-events','auto')
            .on('click', boundedThis);

    }

    clickSelect(d) {
        console.log(`d x,y:${d.x},${d.y},${d.srcElement.attributes['keytext'].value},${this.foo}`);
    }

    renderData3(input) {
        // you have to bind(this) for callback in order for callback to access this variables
        let boundedThis = (this.renderDataAfterLoad).bind(this);
        let flag = this.readInputFile(input,boundedThis);

        // this doesnt work because not bounded to access this variables in method
        //let flag = this.readInputFile(input,this.renderDataAfterLoad);
        return;
    }
}

const learnD3 = new LearnD3();