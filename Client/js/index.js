var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope,$http) {
	console.log("Hello world");
	// INIT
	document.getElementById("user-mssg")
	  .addEventListener("keyup", function(event) {
	    event.preventDefault();
	    if (event.keyCode == 13) {
	    	$scope.user_input = "";    
	    }
	});
	//


  $scope.notification_possible = false;
  if (("Notification" in window)) {
		if(Notification.permission === "granted") {
  		$scope.notification_possible = true;
  	}
  }
  $scope.notify = function (title,body) {
	  if($scope.notification_possible) {
	  	var options = {
	  		body : body,
	  		icon : '/public/img/term.jpg'
	  	};
	  	var notification = new Notification(title,options);
	  }
  };

  $scope.notifyGrant = function() {
  	Notification.requestPermission(function (permission) {
	      if (permission === "granted") {
	      	var options = {
	      		body : "Thanks for the permission to keep you posted! :) ",
	      		icon : '/public/img/term.jpg'
	      	};
	        var notification = new Notification("Hi from FOO!",options);
	      	$scope.notification_possible == true;
	      }
	  });
  };
});