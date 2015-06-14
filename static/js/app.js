var noqapp = angular.module('accountApp', ['ngCookies','ngRoute']);

noqapp.run(function($http,$cookies,sessionService) {

	$http.defaults.headers.post['X-CSRFToken'] = $cookies.get('csrftoken');

});

// configure our routes
noqapp.config(function($routeProvider,$httpProvider) {

	$httpProvider.interceptors.push('authInterceptor');

		$routeProvider
			// route for the home page
			.when('/', {
				templateUrl : '/account/search/'
			})
			
			.when('/search', {
				templateUrl : '/account/search/'
			})

});
