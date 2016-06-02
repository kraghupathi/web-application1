
var app = angular.module('directoryApp.controllers',[]);
app.controller("users", function($scope,  $http, $routeParams, $route,$window){
    $scope.role_name = $window.role_name;
    $http.get("http://localhost:5000/users").success(function(response){
	$scope.users = response;
    });

});
