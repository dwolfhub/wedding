
const clean   = require('gulp-clean');
const fs      = require('fs');
const gulp    = require('gulp');
const rev     = require('gulp-rev');
const sass    = require('gulp-sass');
const through = require('through2');

gulp.task('default', ['rev']);

gulp.task('js', ['clean-js'], function () {
    return gulp.src('assets/js/index.js')
        .pipe(gulp.dest('public_html/dist'));
});

gulp.task('scss', ['clean-css'], function () {
    return gulp.src('assets/scss/main.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('public_html/dist'));
});

gulp.task('img', ['clean-img'], function () {
    return gulp.src('assets/img/*')
        .pipe(gulp.dest('public_html/dist/'));
});

gulp.task('rev', ['img', 'js', 'scss'], function () {
    return gulp.src('public_html/dist/*.{js,css,png,jpg}')
        .pipe(rev())
        .pipe(gulp.dest('public_html/dist'))
        .pipe((function() {
            return through.obj(function(file, enc, cb) {
                this.push(file);

                if (!file.revOrigPath) {
                    return cb();
                }

                fs.unlink(file.revOrigPath, function (err) {
                    if (err) {
                        console.error(err);
                    }

                    cb();
                });
            });
        })())
        .pipe(rev.manifest())
        .pipe(gulp.dest('public_html/dist'))
});

gulp.task('clean-js', function () {
    return gulp.src('public_html/dist/*.js', {read: false})
        .pipe(clean());
});

gulp.task('clean-css', function () {
    return gulp.src('public_html/dist/*.css', {read: false})
        .pipe(clean());
});

gulp.task('clean-img', function () {
    return gulp.src('public_html/dist/*.{png,jpg}', {read: false})
        .pipe(clean());
});

