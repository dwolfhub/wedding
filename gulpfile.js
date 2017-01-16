
const clean   = require('gulp-clean');
const fs      = require('fs');
const gulp    = require('gulp');
const rev     = require('gulp-rev');
const sass    = require('gulp-sass');
const through = require('through2');

const publicDir = 'wedding/page/static/page';
const templatesDir = 'wedding/page/templates/page';

const distDir = publicDir;


let hasFileExtension = function (fileName, ext) {
    return fileName.substr(fileName.length - ext.length) === ext;
};

let replaceInFile = function (fileName, revvedFiles) {
    return function (err, data) {
        if (err) {
            return;
        }

        for (let j in revvedFiles) {
            if (revvedFiles.hasOwnProperty(j)) {
                let fileInfo = j.split('.');

                data = data.replace(
                    new RegExp(
                        fileInfo[0] + '-?.*\.' + fileInfo[1],
                        'g'
                    ),
                    revvedFiles[j]
                );
            }
        }

        fs.writeFile(fileName, data, 'utf8');
    };
};

gulp.task('watch', function () {
    gulp.watch('assets/**/*', ['default']);
});

gulp.task('default', ['favicon', 'img', 'js', 'scss'], function () {
    return gulp.src(distDir + '/*.{js,css,png,jpg,jpeg,html}')
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

                let revvedFiles = JSON.parse(file._contents.toString());

                fs.readFile(templatesDir + '/layout.html', 'utf8', replaceInFile(templatesDir + '/layout.html', revvedFiles));

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
gulp.task('favicon', ['clean-favicon'], function () {
    return gulp.src('assets/favicon/*')
        .pipe(gulp.dest(distDir));
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
gulp.task('clean-favicon', function () {
    return gulp.src(distDir + '/../{apple*,android*,browser*,favicon*,manifest.json,ms-icon*}')
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
    return gulp.src(distDir + '/*.{png,jpg,jpeg}', {read: false})
        .pipe(clean());
});

