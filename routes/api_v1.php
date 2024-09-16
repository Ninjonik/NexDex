<?php

use App\Http\Controllers\api\v1\ExampleController;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\DiscordOAuthController;

/*
|--------------------------------------------------------------------------
| API v1 Routes
|--------------------------------------------------------------------------
|
| This file contains all of the v1 routes.
| This file is loaded and the routes are pre-pended automatically 
| by App\Providers\RouteServiceProvider->boot()
|
*/

// Authenticated API (sanctum)
Route::group([
    'middleware' => ['api_authenticated']
], function() {

    Route::get('/example-authenticated', [ExampleController::class, 'authenticated']);

});

// Public API
Route::group([
    'middleware' => ['api_public'],
], function () {

    Route::get('/example', [ExampleController::class, 'index']);

    // Auth API
    Route::group([
        'prefix' => 'auth'
    ], function () {
        Route::post('login', 'AuthController@login');
        Route::post('logout', 'AuthController@logout');
        Route::post('refresh', 'AuthController@refresh');
        Route::post('me', 'AuthController@me');
        Route::get('discord', [DiscordOAuthController::class, 'redirectToDiscord']);
        Route::get('discord/callback', [DiscordOAuthController::class, 'handleCallback']);
    });

});



