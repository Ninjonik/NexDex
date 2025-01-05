<?php

use App\Http\Controllers\BattleController;
use App\Http\Controllers\CountryballController;
use App\Http\Controllers\DataController;
use App\Http\Controllers\DiscordOAuthController;
use App\Http\Controllers\DroppedCountryballController;
use App\Http\Controllers\GuildController;
use App\Http\Controllers\UserController;
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

    // Guild API
    Route::group([
        'prefix' => 'guild'
    ], function () {
        Route::get('/', [GuildController::class, 'getData']);
        Route::post('/', [GuildController::class, 'postData']);
        Route::get('/{id}', [GuildController::class, 'getData']);
        Route::post('/{id}', [GuildController::class, 'patchData']);
        Route::delete('/{id}', [GuildController::class, 'deleteData']);
    });

    // Battle API
    Route::group([
        'prefix' => 'battle'
    ], function () {
        Route::get('/', [BattleController::class, 'getData']);
        Route::post('/', [BattleController::class, 'postData']);
        Route::get('/{id}', [BattleController::class, 'getData']);
        Route::post('/{id}', [BattleController::class, 'patchData']);
        Route::delete('/{id}', [BattleController::class, 'deleteData']);
    });

    // User API
    Route::group([
        'prefix' => 'user'
    ], function () {
        Route::get('/', [UserController::class, 'getData']);
        Route::post('/', [UserController::class, 'postData']);
        Route::get('/{id}', [UserController::class, 'getData']);
        Route::post('/{id}', [UserController::class, 'patchData']);
        Route::delete('/{id}', [UserController::class, 'deleteData']);
    });

    // Dropped Countryball API
    Route::group([
        'prefix' => 'dropped'
    ], function () {
        Route::get('/', [DroppedCountryballController::class, 'getData']);
        Route::post('/', [DroppedCountryballController::class, 'postData']);
        Route::get('/{id}', [DroppedCountryballController::class, 'getData']);
        Route::post('/{id}', [DroppedCountryballController::class, 'patchData']);
        Route::delete('/{id}', [DroppedCountryballController::class, 'deleteData']);
    });

    // Dropped Countryballs API
    Route::group([
        'prefix' => 'droppedBalls'
    ], function () {
        Route::get('/', [DroppedCountryballController::class, 'getDatas']);
        Route::get('/{id}', [DroppedCountryballController::class, 'getDatas']);
    });

    // Countryball API
    Route::group([
        'prefix' => 'countryball'
    ], function () {
        Route::get('/', [CountryballController::class, 'getData']);
        Route::post('/', [CountryballController::class, 'postData']);
        Route::get('/{id}', [CountryballController::class, 'getData']);
        Route::post('/{id}', [CountryballController::class, 'patchData']);
        Route::delete('/{id}', [CountryballController::class, 'deleteData']);
    });

    // Countryballs API
    Route::group([
        'prefix' => 'countryballs'
    ], function () {
        Route::get('/', [CountryballController::class, 'getDatas']);
        Route::get('/{id}', [CountryballController::class, 'getDatas']);
    });

});



