<?php

namespace App\Http\Controllers;

use App\Models\Guild;
use Config;
use Exception;
use Illuminate\Http\Request;
use Log;

class GuildController extends Controller
{

    public function postData(Request $request)
    {
        $token = $request->header("Authorization");
        if (!$this->verifyToken($token)) {
            return response()->json(["error" => "Invalid token"], 401);
        }

        $result = json_decode($request->getContent(), true);
        $id = $result["id"] ?? "";
        if (empty($id)) {
            return response()->json(["error" => "Invalid input arguments: missing id."], 401);
        }
        $name = $result["name"] ?? "";
        $description = $result["description"] ?? "";

        $model = new Guild();

        // Populate model properties
        $model->id = $id;
        $model->name = $name;
        $model->description = $description;

        // Save model
        $model->save();

        return response()->json(["message" => "Data saved successfully"]);
    }

    private function verifyToken(string $token)
    {
        $internalToken = Config::get('app.internal_api_token');
        $token = substr($token, 7);
        if ($token === $internalToken) {
            return true;
        } else {
            return false;
        }
    }

    public function patchData(Request $request)
    {
        $id = intval($request->route('id'));

        // Verify token and extract data
        $token = $request->header("Authorization");
        if (!$token || !str_starts_with($token, "Bearer ")) {
            return response()->json(["error" => "Invalid token"], 401);
        }

        if (!$this->verifyToken($token)) {
            return response()->json(["error" => "Invalid token"], 401);
        }

        $model = new Guild();

        // Fetch the model data
        $data = $model::find($id);

        if (empty($data)) {
            return response()->json(["error" => "No data found for this guild."], 404);
        }

        $result = json_decode($request->getContent(), true);
        $name = $result["name"] ?? "";
        $description = $result["description"] ?? "";

        // Populate model properties
        $model->name = $name;
        $model->description = $description;

        // Save model
        $data->save();

        return response()->json(["message" => "Data saved successfully"]);
    }

    public function deleteData(Request $request)
    {
        $token = $request->header("Authorization");
        $id = intval($request->route('id'));

        if (!$token || !str_starts_with($token, "Bearer ")) {
            return response()->json(["error" => "Invalid token"], 401);
        }

        if (!$this->verifyToken($token)) {
            return response()->json(["error" => "Invalid token"], 401);
        }

        $model = new Guild();

        try {
            // Fetch the model data
            $data = $model::find($id);

            if (empty($data)) {
                return response()->json(["error" => "No data found for this guild."], 404);
            }

            $data->delete();

            return response()->json($data);
        } catch (Exception $e) {
            Log::error("Error deleting data for guild: $id: " . $e->getMessage());
            return response()->json(["error" => "An error occurred while deleting data."], 500);
        }
    }

    public function getData(Request $request)
    {
        $id = intval($request->route('id') ?? -1);
        $token = $request->header("Authorization");

        if (!$token || !str_starts_with($token, "Bearer ")) {
            return response()->json(["error" => "Invalid token"], 401);
        }

        if (!$this->verifyToken($token)) {
            return response()->json(["error" => "Invalid token"], 401);
        }

        $model = new Guild();

        try {
            // Fetch the model data
            if ($id !== -1) {
                $data = $model::find($id);
            } else {
                $data = $model->all();
            }

            if (empty($data)) {
                return response()->json(["error" => "No data found/for this guild."], 404);
            }

            return response()->json($data);
        } catch (Exception $e) {
            Log::error("Error fetching data for guild $id: " . $e->getMessage());
            return response()->json(["error" => "An error occurred while fetching data."], 500);
        }
    }
}
