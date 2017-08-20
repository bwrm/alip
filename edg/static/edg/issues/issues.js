var fs = require('fs'),
    baseUrl = 'http://issues.wenzhixin.net.cn/bootstrap-table/';

fs.readdir('./', function (err, list) {
    if (err) {
        console.log(err);
        return;
    }
    var content = fs.readFileSync('../sofa.conf').toString(),
        html = [];

    list.sort().forEach(function (file) {
        if (/^\d+.html$/.test(file)) {
            var content = fs.readFileSync(file).toString(),
                m = content.match(/<title>(.*)<\/title>/);

            if (m) {
                html.push('<li><a href="issues/' + file + '">',
                    file.split('.')[0] + '. ' + m[1],
                    '</a></li>');
            }
        }
    });
    fs.writeFileSync('../sofa', content.replace('@@list@@', html.join('\n')));
});
