'use strict';

let debug = false;
let yearCommon = { 1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31 }
let yearLeap =   { 1:31,2:29,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31 } 

let fIsLeapYear = function(yyyy) {
  if(yyyy % 4 != 0) {
    return false;
  } else if (yyyy % 100 != 0) {
    return true;
  } else if (yyyy % 400 != 0) {
    return false;
  } else {
    return true;
  }
}

function SDate(dd,mm,yyyy) {
  this.dd = dd;
  this.mm = mm;
  this.yyyy = yyyy;
}

let fGenDates = function(begDate,endDate) {
  let dd = begDate.dd;
  let mm = begDate.mm;
  let yyyy = begDate.yyyy;
  
  if(debug) {
    console.log(`edate: ${endDate.dd}:${endDate.mm}:${endDate.yyyy}`);
  }

  let structYear = fIsLeapYear(yyyy) ? yearLeap : yearCommon;

  let res = [];

  while(yyyy != endDate.yyyy || mm != endDate.mm || dd != endDate.dd) {
    let sDD = String(dd).padStart(2,'0');
    let sMM = String(mm).padStart(2,'0');
    let sYYYY = String(yyyy);
    let sDate = sDD + sMM + sYYYY;
    res.push(sDate);

    dd++;
    if(dd > structYear[mm]) {
      dd = 1;
      mm++;
      if(mm > 12) {
        mm = 1;
        yyyy++;
        structYear = fIsLeapYear(yyyy) ? yearLeap : yearCommon;
      }
    }
    if(debug) {
      console.log(`${sDD}:${sMM}:${sYYYY} ${sDate}`);  
      console.log(`${sDD}:${sMM}:${sYYYY}    ${dd}:${mm}:${yyyy}`);
    }
  }

  if(debug) {
    console.log(`yyyy:${yyyy} eyyyy:${endDate.yyyy} mm:${mm} emm:${endDate.mm} dd:${dd} edd:${endDate.dd}`);
  }

  return res;
}

let fStart = function() {
  const args = process.argv;
  for(let i = 0; i < args.length; i++) {
    console.log('cmd arg: ' + i + ' -> ' + process.argv[i]);
  }
  
  let lArgs = args.slice(2);  // remove the first 2 args
  let begDate = new SDate(19,9,2020);
  let endDate = new SDate(31,10,2020);
  let lDates = fGenDates(begDate,endDate);
  for(let sDate of lDates) {
    console.log(`* ${sDate}`);
  }
}

fStart();




