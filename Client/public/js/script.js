var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope,$http) {
	$scope.current_tab = 1;
	var textMap = [];
	$scope.textMap = textMap;
	for(i=0;i<3;i++){
		textMap.push([]);
	}
	for(i=0;i<3;i++){
		var texts = textMap[i];
		var text = {
			"date" : i,
			"name" : "bot",
			"isbot" : true,
			"receiver" : "user",
			"time" : "anytime",
			"textdata"  :" hello rammante!!"
		};
		texts.push(text);
		text = {
			"date" : i,
			"name" : "user",
			"isbot" : false,
			"receiver" : "bot",
			"time" : "anytime",
			"textdata"  :" bye bye!!"
		};
		texts.push(text);	
	}


	$scope.check_key = function() {
		if( $scope.event.keyCode == 13) {
			console.log($scope.message_text);
			console.log($scope.current_tab);
			var text = {
			"date" : i,
			"name" : "user",
			"isbot" : false,
			"receiver" : "bot",
			"time" : "just now",
			"textdata"  :$scope.message_text
			};
			$scope.textMap[$scope.current_tab-1].push(text);
			// send text over to server
			var url;
			if($scope.current_tab == 1){
				url = 'http://127.0.0.1:8000/nlp/chatbot/'
			}
			else if($scope.current_tab==2){
				url = 'http://127.0.0.1:8000/nlp/codingmate/'
			}
			else if($scope.current_tab==3){
				url = 'http://127.0.0.1:8000/nlp/scrape/'
			}
			$http({
				'method' 	: 'POST',
				'url'		: url,
				'data'		: text,
			})
			.then(function (resp){
				console.log(resp);
				var bot_text = {

				};
				// $scope.textMap[$scope.current_tab-1].push(bot_text);
			}, function (err){
				console.log(err);
			});
			$scope.message_text = "";
		}
	}
});