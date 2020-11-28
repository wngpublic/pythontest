let yargs = require('yargs');
let args = yargs.argv;

for(let i = 0; i < process.argv.length; i++){
    console.log(`${i}: ${process.argv[i]}`);
}

// node testcmdline.js --id1=xyz --abc=efg // -id1=xyz doesnt work
if(args.id1 !== undefined) {
    console.log(`id1: ${args.id1}`);
}
