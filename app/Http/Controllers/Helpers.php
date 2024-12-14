<?php

namespace App\Http\Controllers;

use Config;

class Helpers extends Controller
{
    public static function verifyToken(string $token)
    {
        $internalToken = Config::get('app.internal_api_token');
        $token = substr($token, 7);
        if ($token === $internalToken) {
            return true;
        } else {
            return false;
        }
    }

    public static function isAnyEmpty(array $array): bool
    {
        foreach ($array as $element) {
            if (!is_array($element)) {
                // Check if the current element is empty
                if (!$element ?? '') {
                    return true;
                }
            } else {
                // Recursively check nested arrays
                if (!areAllElementsFull($element)) {
                    return true;
                }
            }
        }

        return false;
    }
}
