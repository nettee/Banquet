var rp = require('request-promise');

var data_url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=hb&ft=&rs=&gs=0&sc=1nzf&st=desc&pi=1&pn=50&mg=a&dx=1&v=0.9969968529161948';

rp(data_url)
    .then(function (htmlString) {
        data = JSON.parse(htmlString);
        console.log(data);
    })
    .catch(function (err) {
        console.log(err);
    });
