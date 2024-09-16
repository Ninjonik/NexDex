<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class Authentication
{
    public function handle(Request $request, Closure $next)
    {
        $token = $request->cookie('token');

        if (empty($token)) {
            return response()->json(['error' => 'Unauthenticated.'], 401);
        }
        // TODO: Validate token

        return $next($request);
    }
}
