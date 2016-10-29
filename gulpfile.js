
const clean   = require('gulp-clean');
const fs      = require('fs');
const gulp    = require('gulp');
const rev     = require('gulp-rev');
const sass    = require('gulp-sass');
const through = require('through2');

const distDir = 'public_html/dist';


let hasFileExtension = function (fileName, ext) {
    return fileName.substr(fileName.length - ext.length) === ext;
};

let replaceInFile = function (fileName, revvedFiles) {
    return function (err, data) {
        if (err) {
            return;
        }

        for (let j in revvedFiles) {    
            data = data.replace(new RegExp(j, 'g'), revvedFiles[j]);
        }

        fs.writeFile(fileName, data, 'utf8');
    };
};

gulp.task('watch', function () {
    gulp.watch('assets/**/*', ['default']);
});

gulp.task('default', ['html', 'img', 'js', 'scss'], function () {
    return gulp.src(distDir + '/*.{js,css,png,jpg,html}')
        .pipe(rev())
        .pipe(gulp.dest(distDir))
        .pipe((function () {
            // deleting originals 
            return through.obj(function(file, enc, cb) {
                this.push(file);

                if (!file.revOrigPath || hasFileExtension(file.revOrigPath, 'html')) {
                    return cb();
                }

                fs.unlink(file.revOrigPath, function (err) {
                    cb();
                });
            });
        })())
        .pipe(rev.manifest())
        .pipe((function () {
            // replacing non-revved file names with revved
            return through.obj(function (file, enc, cb) {
                this.push(file);

                let revvedFiles = JSON.parse(file._contents.toString()),
                    fileNames = ['public_html/index.html', 'public_html/hotels.html', 'public_html/venue.html', 'public_html/wedding-day-info.html'],
                    i;

                for (i = 0; i < fileNames.length; i++) {
                    fs.readFile(fileNames[i], 'utf8', replaceInFile(fileNames[i], revvedFiles));
                }

                fs.readdir(distDir + '/', function (err, files) {
                    let filesLength = files.length,
                        i;

                    for (i = 0; i < filesLength; i++) {
                        if (hasFileExtension(files[i], 'png') || hasFileExtension(files[i], 'jpg')) {
                            continue;
                        }

                        fileName = distDir + '/' + files[i];

                        fs.readFile(fileName, 'utf8', replaceInFile(fileName, revvedFiles));
                    }
                });

                cb();
            });
        })())
        .pipe(gulp.dest(distDir))
});

/* Compile and Move Tasks */

gulp.task('html', ['clean-html'], function () {
    return gulp.src('assets/html/*.html')
        .pipe(gulp.dest(distDir + '/../'));
});

gulp.task('js', ['clean-js'], function () {
    return gulp.src('assets/js/index.js')
        .pipe(gulp.dest(distDir));
});

gulp.task('scss', ['clean-css'], function () {
    return gulp.src('assets/scss/main.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest(distDir));
});

gulp.task('img', ['clean-img'], function () {
    return gulp.src('assets/img/*')
        .pipe(gulp.dest(distDir));
});

/* Cleaning Tasks */

gulp.task('clean-html', function () {
    return gulp.src(distDir + '/../*.html', {read: false})
        .pipe(clean());
});

gulp.task('clean-js', function () {
    return gulp.src(distDir + '/*.js', {read: false})
        .pipe(clean());
});

gulp.task('clean-css', function () {
    return gulp.src(distDir + '/*.css', {read: false})
        .pipe(clean());
});

gulp.task('clean-img', function () {
    return gulp.src(distDir + '/*.{png,jpg}', {read: false})
        .pipe(clean());
});

