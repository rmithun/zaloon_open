noqapp.directive('facebook', function($http,httpServices) {
  return {
    restrict: 'A',
    scope: true,
    controller: function($scope, $attrs) {
      // Load the SDK Asynchronously
      (function(d){
        var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
        if (d.getElementById(id)) {return;}
        js = d.createElement('script'); js.id = id; js.async = true;
        js.src = "https://connect.facebook.net/en_US/sdk.js"; 
        ref.parentNode.insertBefore(js, ref);
      }(document));

    
      $scope.fetch = function() {

        FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
          // the user is logged in and has authenticated your
          // app, and response.authResponse supplies
          // the user's ID, a valid access token, a signed
          // request, and the time the access token 
          // and signed request each expire
          var uid = response.authResponse.userID;
          $scope.fbLogin(response.authResponse.accessToken)
        } 
        else
        {
          FB.login(function(response) {

           // console.log(response)
            if (response.authResponse) {
              //console.log(response)
              $scope.login_status =  response.status
              $scope.fbLogin(response.authResponse.accessToken)
              console.log('FB.login connected');
            } else {
              console.log('FB.login cancelled');
            }
            }, { scope: 'email,user_location,user_birthday'});
        }
      });
        
      };
    },
    link: function(scope, element, attrs, controller) {
      // Additional JS functions here
      window.fbAsyncInit = function() {
        FB.init({
          appId      : attrs.facebook, // App ID
          channelUrl : 'http://localhost/static/js/channel.html', // Channel File
          //channelUrl : 'http//zaloon.in/static/js/channel.html', // Channel File
          status     : true, // check login status
          cookie     : true, // enable cookies to allow the server to access the session
          xfbml      : true,  // parse XFBML
          version    : 'v2.4'
        });
      }; // end of fbAsyncInit
    }
  }
});



// Phone Number Formatting Directive
noqapp.directive("phoneformat", function() {
    return {
        restrict: "A",
        require: "ngModel",
        link: function(scope, element, attr, ngModelCtrl) {
            var phoneParse = function(value) {
                var numbers = value && value.replace(/-/g, "");
                if (/^\d{10}$/.test(numbers)) {
                    return numbers;
                }

                return undefined;
            }
            var phoneFormat = function(value) {
                var numbers = value && value.replace(/-/g, "");
                var matches = numbers && numbers.match(/^(\d{3})(\d{3})(\d{4})$/);

                if (matches) {
                    return matches[1] + "-" + matches[2] + "-" + matches[3];
                }

                return undefined;
            }
            ngModelCtrl.$parsers.push(phoneParse);
            ngModelCtrl.$formatters.push(phoneFormat);

            element.bind("blur", function() {
                var value = phoneFormat(element.val());
                var isValid = !!value;
                if (isValid) {
                    ngModelCtrl.$setViewValue(value);
                    ngModelCtrl.$render();
                }

                ngModelCtrl.$setValidity("mobileno", isValid);
                scope.$apply();
            });
        }
    };
});

