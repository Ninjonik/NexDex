<?php
namespace App\Services;
use App\Models\User;
use Illuminate\Support\Facades\Auth;
use Tymon\JWTAuth\Exceptions\JWTException;
use Tymon\JWTAuth\Facades\JWTAuth;

class JWTService{

    public static function generate() {
        $user = Auth::user();
        return JWTAuth::fromUser($user);
    }

    public static function verifyToken($token)
    {
        try {
//            JWTAuth::decode($token);
            JWTAuth::setToken($token);
            JWTAuth::authenticate();
            return true;
        } catch (JWTException $e) {
            return false;
        }
    }

    public static function getUserData($request)
    {
        $token = $request->header('Authorization');

        if (!$token) {
            return response()->json(['error' => 'Token not provided'], 401);
        }

        $tokenParts = explode(' ', $token);
        if (count($tokenParts) !== 2 || $tokenParts[0] !== 'Bearer') {
            return response()->json(['error' => 'Invalid token format'], 401);
        }

        $token = $tokenParts[1];

        if (!self::verifyToken($token)) {
            return response()->json(['error' => 'Invalid token'], 401);
        }

        $payload = JWTAuth::getPayload();

        if (!$payload) {
            return response()->json([
                'message' => 'User not found'
            ], 404);
        }

        try {
            $userId = $payload['sub'];
            $user = User::findOrFail($userId);
            return response()->json(['user' => $user], 200);
        } catch (\Exception $e) {
            return response()->json(['error' => 'User not found'], 404);
        }
    }

    public static function refresh($token) {
        try {
            return JWTAuth::refresh($token);
        } catch(JWTException $e) {
            return false;
        }
    }
}