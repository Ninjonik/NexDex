<?php

use App\Http\Controllers\DataController;
use App\Http\Controllers\DiscordOAuthController;
use Illuminate\Support\Facades\Route;

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
/*
Route::group([
    'middleware' => ['api_authenticated']
], function() {

    Route::get('/example-authenticated', [ExampleController::class, 'authenticated']);

});
*/

// Public API
Route::group([
    'middleware' => ['api_public'],
], function () {
    // Auth API
    Route::group([
        'prefix' => 'auth'
    ], function () {
        Route::get('user', [DiscordOAuthController::class, 'getUserData']);
        Route::get('discord', [DiscordOAuthController::class, 'redirectToDiscord']);
        Route::get('discord/callback', [DiscordOAuthController::class, 'handleCallback']);
    });

    // Data API
    Route::group([
        'prefix' => 'data'
    ], function () {
        Route::get('/{type}', [DataController::class, 'getData']);
        Route::post('/{type}', [DataController::class, 'postData']);
        Route::get('/{type}/{id}', [DataController::class, 'getData']);
        Route::post('/{type}/{id}', [DataController::class, 'patchData']);
        Route::delete('/{type}/{id}', [DataController::class, 'deleteData']);
    });

});



