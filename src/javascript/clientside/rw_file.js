
class FileRW {
    constructor() {
        this.fileinputText = null;
    }
    readInputFile(input) {
        try {
            let filei = document.getElementById('file-selector-i').files[0];
            if(filei == null) {
                document.getElementById('jstxt').innerHTML = `no filename detected!`;
                return;
            }
            let fileReader = new FileReader();
            fileReader.readAsText(filei);
            fileReader.onload = () => {
                this.fileinputText = fileReader.result;
                //document.getElementById('jstxt').innerHTML = '<pre>' + this.fileinputText + '</pre>'; // json needs <pre>
                document.getElementById('id-p-right').innerHTML ='<pre>' + this.fileinputText + '</pre>'; // json needs <pre>
            };
            fileReader.onerror = () => {
                console.log(`error reading ${filei}`);
            }
        } catch(e) {
            console.log(e);
        }
    }
    saveInputFile(input) {
        try {
            if(this.fileinputText == null) {
                document.getElementById('jstxt').innerHTML = `no filename detected!`;
                return;
            }
            let filename = 'tmpfile.txt';
            //localStorage.setItem(filename, this.fileinputText);
            sessionStorage.setItem(filename, this.fileinputText);
            let a = document.createElement('a')
            let blob = new Blob([sessionStorage.getItem(filename)],{type:'text/plain'});
            a.href = window.URL.createObjectURL(blob); // blob only!
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            sessionStorage.removeItem(filename);
            //localStorage.removeItem(filename);
        } catch(e) {
            console.log(e);
        }
    }
}

filerw = new FileRW();

