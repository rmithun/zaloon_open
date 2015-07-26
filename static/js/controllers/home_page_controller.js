noqapp.controller('homepagecontroller',function($scope, $cookies, $location,httpServices,sessionService,putResultService){
$scope.is_logged = sessionService.isLogged();
$scope.formsubmit=false;

 function getFBKey()
 {
	httpServices.getFBKey().then(function(data)
	{
		$scope.fb_key = data['fb_key'].data
	});
 }
getFBKey()

	$scope.fbLogin = function(dummy)
	{

		httpServices.loginUsingFB(dummy).then(function(data)
		{
		  if(data)
		  {
		  	sessionService.setAuthToken(data)
		  	httpServices.getUsrDetails().then(function(dataz)
		  	{
		  		$scope.is_logged = sessionService.isLogged()
		  		$scope.user_name = dataz['user_details'].data[0].first_name
		  		//$('#signupmodel').modal('hide');
		  	}, function()
		  	{
		  		$scope.is_logged = sessionService.isLogged()
		  		console.log("Error getting user data")
		  	})
		  	
		  }
		},function()
		{
		   //cannot login to fb try again
		   console.log("Cannot login to FB")
		});
	}

if(sessionService.isLogged())
{
httpServices.getUsrDetails().then(function(dataz)
{
	$scope.user_name = dataz['user_details'].data[0].first_name
}, function()
{
	console.log("Error getting user data")	
})	
}


	$scope.logOut = function()
	{	
		httpServices.logOut().then(function(logout_data)
		{
			$cookies.remove('token')
			//$scope.is_logged = sessionService.isLogged()
			console.log("Logged out successfully")
			$window.location.href = "/"
		},
		function()
		{
			console.log("Logout Error")
		})
	}


	//AutoComplete
	$scope.searchdata_ = {};	
	$scope.searchdata_['arealist'] = [];	
	var acService = new google.maps.places.AutocompleteService();
	$scope.areacomplete = function () {		
    	if ($scope.searchdata_['searchlocation'] != "" && typeof $scope.searchdata_['searchlocation'] != 'undefined') {
            acService.getPlacePredictions({
                input: $scope.searchdata_['searchlocation'],
                types: ['(regions)'],
                componentRestrictions: { 'country': 'in' }
            }, function (places, status) {
                if (status === google.maps.places.PlacesServiceStatus.OK) {                    
                    var _places = [];                    
                    for (var i = 0; i < places.length; ++i) {
                    	_places.push({
                        	id: places[i].place_id,
                        	value: places[i].description,
                        	label: places[i].description
                    	});
                	}                	
                	$scope.searchdata_['arealist'] = _places;     
            	}
        	});
    	}
    }
    //Get All Services    
    $scope.searchdata_['servicelist']='';
    httpServices.getService().then(function(data)
    	{    		
    		$scope.searchdata_['servicelist'] = data['service_details'].data;

    	},function()
    	{
    		console.log("Try again to get service")
    	});    

    //Search Studio Details Event
    $scope.searchstudio=function(form){
    	$scope.formsubmit=true;
    	if(form.$valid)
		{ 			
			var obj={'service':$scope.searchdata_.service_name,'location':$scope.searchdata_.searchlocation};
			$('.loader-overlay').show();
			 httpServices.getstudioDetails(obj).then(function(data)
		    	{		
		    		$cookies.putObject('searchdata',obj,{path:'/'})    	
		    		//console.log(data.studio_details.data)	
		    		//$cookies.putObject('data',data.studio_details.data,{path:'/'})
		    		putResultService.setresult(data.studio_details.data);
		    		$location.path("/search");		    		
		    	},function()
		    	{
		    		console.log("Try again to get service")
		    	});
		}
    }
    $scope.onserviceselect = function ($item, $model, $label) {    	
	    $scope.searchdata_.service_name=$item.service_name;	   
	};
	$scope.onlocationselect = function ($item, $model, $label) {
		$scope.searchdata_.searchlocation=$label;
	};
});