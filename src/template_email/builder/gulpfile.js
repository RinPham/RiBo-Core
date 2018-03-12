var gulp = require('gulp');
var emailBuilder = require('gulp-email-builder');
var templateCompiler = require('./lib/compiler');
var utils = require('./lib/utils');
var configs = require('./config.json');
var run = require('run-sequence');
var paths = configs.paths;
var fs = require('fs');
var options = configs.options;
var through = require('through2');

gulp.task('build_email', function () {
    gulp.src(paths.html_source)
        .pipe(emailBuilder(options.builder))
        .pipe(gulp.dest(paths.tmpl));
});

gulp.task('compile_email', function () {
    return gulp.src(paths.tmpl_source)
        .pipe(fixBasePath({
            '_find': 'emails/base.html',
            '_replaceBy': 'base.html'
        }))
        .pipe(templateCompiler(options.compiler))
        .pipe(gulp.dest(paths.rendered))
});

/*
gulp.task('fix_path', function () {
    return gulp.src(paths.tmpl_source)
        .pipe(fixBasePath({
            '_find': 'base.html',
            '_replaceBy': 'emails/base.html'
        }))
        .pipe(gulp.dest(function (file) {
            return file.base;
        }));
});
*/

function fixBasePath(opts) {
    return through.obj(function (file, enc, cb) {
        if (file.isBuffer()) {
            var html = file.contents.toString();
            html = html.replace(opts._find, opts._replaceBy);
            file.contents = new Buffer(html);
            cb(null, file);
        }
    });
}


gulp.task('process', function () {
    run('build_email', function () {
        setTimeout(function () {
            run('compile_email', function (a, b) {
                //run('fix_path');
            })
        }, 500);
    });
});

gulp.task('watch', function () {
    gulp.watch(configs.watch, ['process']);
});

gulp.task('default', ['watch', 'process']);