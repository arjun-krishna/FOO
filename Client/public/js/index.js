var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope,$http) {

	$scope.mode_style = [{},{},{}];
	$scope.tab_show = [true,false,false];

	$scope.mode = function (i) {
		$scope.mode_style[i] = {'background-color' : 'lightblue'};
		for(var j=0;j<3;j++) {
			if(j!=i) {
				$scope.mode_style[j] = {};
				$scope.tab_show[j] = false;
			}
		}
		$scope.tab_show[i] = true;
	}

	$scope.check_key = function() {
		if( $scope.event.keyCode == 13) {
			console.log($scope.user_input);
			$scope.user_input = "";
		}
	} 

  $scope.notify = function (title,body) {
	  if (("Notification" in window)) {
			if(Notification.permission === "granted") {
	  		var options = {
		  		body : body,
		  		icon : 'img/term.jpg'
		  	};
		  	var notification = new Notification(title,options);	
	  	} else {
	  		console.log("TEST!");
	  		Notification.requestPermission(function (permission) {
		      if (permission === "granted") {
		      	var options = {
		      		body : "Thanks for the permission to keep you posted! :) ",
		      		icon : 'img/term.jpg'
		      	};
		        var notification = new Notification("Hi from FOO!",options);
		      	$scope.notification_possible == true;
		      }
			  });
	  	}
	  }
  };

  $scope.testnlp = function (){
  	if($scope.search_string.length != 0){
  		$http({
  			'method'	: 'POST',
  			'url'			: 'http://127.0.0.1:8000/nlp/scrape/',
  			'data'		: {'string' : $scope.search_string }	
  		})
  		.then(function (resp){
  			console.log(resp.data);
  		}, function (err){
  			console.log(err);
  		});
  	}
  	else {
  		alert("length 0");
  	}
  }

});