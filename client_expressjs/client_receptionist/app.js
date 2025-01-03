var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var hbs = require('hbs');
var paginate = require('handlebars-paginate');
var helpers = require("../shared/utils/helpers");
require('dotenv').config({ path: '../.env' });

var app = express();

var auth_middleware = require('../shared/services/middleware');
var indexRouter = require('./routes/index');

// view engine setup
app.set('views', path.join('../shared/views/'));
app.set('view engine', 'hbs');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join('../shared/public')));
hbs.registerPartials('../shared/views/partials');
hbs.registerHelper('paginate', paginate);
hbs.registerHelper("if_eq", helpers.if_eq); 
hbs.localsAsTemplateData(app);

app.use(auth_middleware.auth);
app.use('/', indexRouter);


// catch 404 and forward to error handler
app.use(function (req, res, next) {
  next(createError(404));
});

// error handler
app.use(function (err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
