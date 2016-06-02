
var app = angular.module('directoryApp',['ngRoute','directoryApp.controllers']);
app.config(function($routeProvider){
  $routeProvider
    .when('/', {
      templateUrl : '/static/partials/users.html',
      controller  : 'users'
    });
});
