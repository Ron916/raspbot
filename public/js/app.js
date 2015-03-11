(function(){
    /*
     Cheatsheet:
     ng-submit
     ng-controller="SomethingController as somethingCtrl"
     ng-repeat="model in models"   ex:  <li ng-repeat="model in controller.models">@{{ model.attr }}</li>
     ng-show="controller.attribute"    //shows if != true
     ng-show="var === other"         //shows if expression is true
     <img ng-src="{{ controller.image }}">
     ng-click="something === 4"      {{ something }}
     -or-
     ng-click="controller.method()"

     ng-model="controller.model.attr"   //binds form input to this value

     {{ data | filter:options }}   ex: {{ controller.price | currency }} formats as price
     ng-class="{ cssClass:var === 1 }"           // var === 1 then add css class

     ng-include="'file.html'"    //fetched by ajax

     css:
     .ng-invalid.ng-dirty{}    //if an input is invalid
     .ng-valid.ng-dirty{}        //if an input is valid

     */
    var mrApp = angular.module('mr.app', ['ngRoute','ngAnimate']);

    /**
     * Main Controller for mr.app, covers html body
     */
    mrApp.controller('MainController', function (
        $scope, USER_ROLES, AuthService, Session, Cache, APP_VARS
    ) {
        $scope.currentUser = null;
        $scope.userRoles = USER_ROLES;
        $scope.isAuthorized = AuthService.isAuthorized;

        /**
         * Construct
         */
        $scope.init = function() {};

        $scope.setCurrentUser = function (user) {
            $scope.currentUser = user;
        };

        $scope.init();
    });

    /**
     * LoginController, deals with login widget and user sessions
     */
    mrApp.controller('LoginController', function (
        $scope, $rootScope, AUTH_EVENTS, AuthService, Session, Cache, APP_VARS
    ) {
        $scope.credentials = {
            email: '',
            password: ''
        };

        /**
         * Construct
         */
        $scope.init = function() {
            if (Cache.get(APP_VARS.userInfo)) {
                //if we have cache, attempt to login with the token
                $scope.userInfo = Cache.get(APP_VARS.userInfo);
                AuthService.login($scope.userInfo).then(function(user){
                    $rootScope.$broadcast(AUTH_EVENTS.loginSuccess);
                    $scope.setCurrentUser(user);
                }, function () {
                    $rootScope.$broadcast(AUTH_EVENTS.loginFailed);
                });
            }
        };

        $scope.login = function (credentials) {
            AuthService.login(credentials).then(function (user) {
                $rootScope.$broadcast(AUTH_EVENTS.loginSuccess);
                $scope.setCurrentUser(user);
                //set token to cache
                var cacheUser = {};
                cacheUser.token = user.token;
                cacheUser.email = user.email;
                Cache.set(APP_VARS.userInfo, cacheUser);
            }, function () {
                $rootScope.$broadcast(AUTH_EVENTS.loginFailed);
            });
        };

        $scope.logout = function(){
            Session.destroy();
            $scope.setCurrentUser(null);
            Cache.set(APP_VARS.userInfo, null);
        };

        $scope.init();
    });

    /**
     *
     */
    mrApp.controller('ProfileController', function($scope, Cache, Session){
        //$scope.
    });

    mrApp.directive('sideBarMenu', function(API_ENDPOINTS, APP_VARS){
        var menu = {
            templateUrl: APP_VARS.html + 'side-bar-menu',
            restrict: 'AECM', //(A)ttribute, (E)lement, (C)lass, (M) Comment (allowed)
            replace: false,  //replace entire container? vs place inside
            link: function(scope, elem, attrs) {
                //scope.$apply();
            }
            //,controller: controllerFunction, //Embed a custom controller in the directive
            //,compile: function(tElem,attrs) {
            //do optional DOM transformation here
            //return function(scope,elem,attrs) {
            //linking function here
            //};
            //}
        };

        return menu;
    });

    /**
     * Builds the users menu
     */
    mrApp.controller('SideBarController', function($scope){
        $scope.menu = [
            {
                title: 'Customers',
                link: '#',
                children: [
                    {
                        title: 'All',
                        link: '#'
                    },
                    {
                        title: 'Create',
                        link: '#'
                    }
                ]
            },
            {
                title: 'Jobs',
                link: '#',
                children: [
                    {
                        title: 'All',
                        link: '#'
                    },
                    {
                        title: 'Create',
                        link: '#'
                    }
                ]
            }
        ];
        return $scope;
    });

    /**
     *
     */
    mrApp.config(function($routeProvider, $locationProvider){
        //$routeProvider
        //    .when('/wat', {
        //        templateUrl: 'book.html',
        //        controller: 'BookController',
        //        resolve: {
        //            // I will cause a 1 second delay
        //            delay: function($q, $timeout) {
        //                var delay = $q.defer();
        //                $timeout(delay.resolve, 1000);
        //                return delay.promise;
        //            }
        //        }
        //    })
        //    .when('/Book/:bookId/ch/:chapterId', {
        //        templateUrl: 'chapter.html',
        //        controller: 'ChapterController'
        //    });
    });

    /**
     *
     */
    mrApp.constant('AUTH_EVENTS', {
        loginSuccess: 'auth-login-success',
        loginFailed: 'auth-login-failed',
        logoutSuccess: 'auth-logout-success',
        sessionTimeout: 'auth-session-timeout',
        notAuthenticated: 'auth-not-authenticated',
        notAuthorized: 'auth-not-authorized'
    });

    /**
     *
     */
    mrApp.constant('USER_ROLES', {
        all: '*',
        admin: 'admin',
        user: 'user',
        guest: 'guest'
    });

    /**
     *
     */
    mrApp.constant('APP_VARS', {
        userInfo: 'userInfo',
        html:     VARS.html
    });

    /**
     *
     */
    mrApp.constant('API_ENDPOINTS', {
        endpoint:   VARS.endpoint,
        login:      VARS.login,
        menu:       VARS.menu
    });

    /**
     *
     */
    mrApp.factory('AuthService', function (
        $http, Session, Cache, APP_VARS, API_ENDPOINTS
    ) {
        var authService = {};
        authService.login = function (credentials) {
            return $http
                .post(API_ENDPOINTS.login, credentials)
                .then(function (res) {

                    var user = res.data.data;
                    Session.create(
                        user.id, user.id,
                        user.email, user.role);
                    Cache.set(APP_VARS.userCacheKey, user);
                    return user;
                });
        };
        authService.isAuthenticated = function () {
            return !!Session.userId;
        };
        authService.isAuthorized = function (authorizedRoles) {
            if (!angular.isArray(authorizedRoles)) {
                authorizedRoles = [authorizedRoles];
            }
            return (authService.isAuthenticated() &&
            authorizedRoles.indexOf(Session.userRole) !== -1);
        };
        return authService;
    });

    /**
     * Flashing session storage, mimic laravel Cache facade :D
     */
    mrApp.factory('Cache', function(){
        var Cache = {};
        Cache.set = function(key, data){
            window.sessionStorage[ key ] = JSON.stringify(data);
        };
        Cache.get = function(key, ifNot){
            if(window.sessionStorage[ key ]){
                return JSON.parse(window.sessionStorage[ key ]);
            }
            return ifNot ? ifNot : null;
        };
        return Cache;
    });

    /**
     *
     */
    mrApp.service('Session', function () {
        this.create = function (sessionId, userId, userEmail, userRole) {
            this.id = sessionId;
            this.userId = userId;
            this.userEmail = userEmail;
            this.userRole = userRole;
        };
        this.destroy = function () {
            this.id = null;
            this.userId = null;
            this.userEmail = null;
            this.userRole = null;
        };
        return this;
    });

    /**
     * Part of the fix for some browsers that can't autofill angular forms
     */
    mrApp.directive('formAutofillFix', function ($timeout) {
        return function (scope, element, attrs) {
            element.prop('method', 'post');
            if (attrs.ngSubmit) {
                $timeout(function () {
                    element
                        .unbind('submit')
                        .bind('submit', function (event) {
                            event.preventDefault();
                            element
                                .find('input, textarea, select')
                                .trigger('input')
                                .trigger('change')
                                .trigger('keydown');
                            scope.$apply(attrs.ngSubmit);
                        });
                });
            }
        };
    });

})($);