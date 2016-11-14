var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope,$http) {
	$scope.current_tab = 1;
	var textMap = [];
	$scope.textMap = textMap;
	for(i=0;i<3;i++){
		textMap.push([]);
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
			var lol = new String($scope.message_text);
			$scope.message_text = "";
			// var url;
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
				'data'		: {"string" :lol},
			})
			.then(function (resp){
				console.log(resp);
				var currdate = "Today";
				var bot_text = {
					"date" : currdate,
					"name" : "BOT",
					"isbot" : true,
					"receiver" : "User",
					"time" : "just now",
				};
				if(resp.config.url === 'http://127.0.0.1:8000/nlp/chatbot/'){
					bot_text.textdata = resp.data.string
				}	
				else if(resp.config.url === 'http://127.0.0.1:8000/nlp/scrape/'){
					console.log("pop")
					if(resp.data.error!=null){
						bot_text.errormsg = resp.data.error;
					}
					else {
						// bot_text.data = {}
						bot_text.data = resp.data
					}
					// console.log(bot_text.data.accepted_ans.text)
				}
				$scope.textMap[$scope.current_tab-1].push(bot_text);
				
			}, function (err){
				console.log(err);
			});
			
		}
	}
});