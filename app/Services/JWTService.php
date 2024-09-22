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

    public static function verify($token) {
        try {
            JWTAuth::decode($token);
            return true;
        } catch(JWTException $e) {
            return false;
        }
    }

    public static function getUserData($request)
    {
        $token = $request->header('Authorization');

        if (!$token) {;
            return response()->json(['error' => 'Token not provided'], 401);
        }

        $tokenParts = explode(' ', $token);
        if (count($tokenParts) !== 2 || $tokenParts[0] !== 'Bearer') {
            return response()->json(['error' => 'Invalid token format'], 401);
        }

        $token = $tokenParts[1];

        try {
            JWTAuth::setToken($token);

            $payload = JWTAuth::getPayload();

            if (!$payload) {
                return response()->json([
                    'message' => 'User not found'
                ], 401);
            }

            try {
                $userId = $payload['sub'];

                $user = User::findOrFail($userId);

                return response()->json(['user' => $user], 200);
            } catch (\Exception $e) {
                return response()->json(['error' => 'User not found'], 404);
            }

        } catch (TokenExpiredException $e) {
            return response()->json([
                'message' => 'Token expired',
                'error' => $e
            ], 401);
        } catch (TokenInvalidException $e) {
            return response()->json([
                'message' => 'Invalid token',
                'error' => $e
            ], 401);
        } catch (JWTException $e) {
            return response()->json([
                'message' => 'Token not provided',
                'error' => $e
            ], 401);
        } catch (TokenBlacklistedException $e) {
            return response()->json([
                'message' => 'Token blacklisted',
                'error' => $e
            ], 401);
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