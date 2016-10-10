var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope,$http) {
   $scope.submit = function () {
   		console.log($scope.user_input);
   		$scope.user_input = "";
   } 
});