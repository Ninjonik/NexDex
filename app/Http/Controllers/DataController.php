<?php

namespace App\Http\Controllers;

use App\Models\Faction;
use App\Models\Ability;
use App\Models\Economy;
use App\Models\Ideology;
use App\Models\Regime;
use App\Services\JWTService;
use Illuminate\Http\Request;
use Illuminate\Support\Str;

class DataController extends Controller
{
    public function postData(Request $request)
    {
        // Verify token and extract data
        $token = $request->header("Authorization");
        if (!$token || !str_starts_with($token, "Bearer ")) {
            return response()->json(["error" => "Invalid token"], 401);
        }

        $token = substr($token, 7);
        if (!JWTService::verifyToken($token)) {
            return response()->json(["error" => "Invalid token"], 401);
        }

        $formData = $request->all();
        $name = $formData["name"] ?? null;
        $description = $formData["description"] ?? null;
        $logo = $formData["logo"] ?? null;
        $thumbnail = $formData["thumbnail"] ?? null;
        $type = $request->route('type');

        // Handle file uploads
        $logoHash = $logo
            ? Str::random(32) . "." . $logo->getClientOriginalExtension()
            : null;
        $thumbnailHash = $thumbnail
            ? Str::random(32) . "." . $thumbnail->getClientOriginalExtension()
            : null;

        if ($logo) {
            $logo->storeAs("images/logos", $logoHash, "public");
        }

        if ($thumbnail) {
            $thumbnail->storeAs("images/thumbnails", $thumbnailHash, "public");
        }

        // Create model instance based on type
        $model = match ($type) {
            "factions" => new Faction(),
            "abilities" => new Ability(),
            "economies" => new Economy(),
            "ideologies" => new Ideology(),
            "regimes" => new Regime(),
            default => null,
        };

        if (!$model) {
            return response()->json(["error" => "Invalid model type."], 400);
        }

        // Populate model properties
        $model->name = $name;
        $model->description = $description;
        $model->logo = $logoHash;
        $model->thumbnail = $thumbnailHash;

        // Save model
        $model->save();

        return response()->json(["message" => "Data saved successfully"]);
    }

    public function getData(Request $request)
    {
        $type = $request->route('type');
        $token = $request->header("Authorization");

        if (!$token || !str_starts_with($token, "Bearer ")) {
            return response()->json(["error" => "Invalid token"], 401);
        }

        $token = substr($token, 7);
        if (!JWTService::verifyToken($token)) {
            return response()->json(["error" => "Invalid token"], 401);
        }

        // Create model instance based on type
        $model = match ($type) {
            "factions" => new Faction(),
            "abilities" => new Ability(),
            "economies" => new Economy(),
            "ideologies" => new Ideology(),
            "regimes" => new Regime(),
            default => null,
        };

        if (!$model) {
            return response()->json(["error" => "Invalid model type."], 400);
        }

        try {
            // Fetch the model data
            $data = $model->all();

            if (empty($data)) {
                return response()->json(["error" => "No data found for this type."], 404);
            }

            return response()->json($data);
        } catch (\Exception $e) {
            \Log::error("Error fetching data for {$type}: " . $e->getMessage());
            return response()->json(["error" => "An error occurred while fetching data."], 500);
        }
    }
}
