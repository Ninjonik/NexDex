<?php

namespace App\Http\Controllers;

use Exception;
use Illuminate\Http\Request;
use Log;

class APIController extends Controller
{
    protected $model = null;

    public function setModel($modelName)
    {
        $this->model = new $modelName();
    }

    public function postData(Request $request)
    {
        $token = $request->header("Authorization");
        if (!Helpers::verifyToken($token)) {
            return response()->json(["error" => "Invalid token"], 401);
        }

        $result = json_decode($request->getContent(), true);

        // Populate model properties
        foreach ($result as $key => $value) {
            try {
                $this->model->$key = $value;
            } catch (e) {
            }
        }

        $this->model->save();

        return response()->json(["message" => "Data saved successfully"]);
    }

    public function patchData(Request $request)
    {
        $token = $request->header("Authorization");
        if (!Helpers::verifyToken($token)) {
            return response()->json(["error" => "Invalid token"], 401);
        }

        $id = intval($request->route('id'));

        $data = $this->model::find($id);

        if (empty($data)) {
            return response()->json(["error" => "No data found for this resource."], 404);
        }

        $result = json_decode($request->getContent(), true);

        // Populate model properties
        foreach ($result as $key => $value) {
            try {
                $data->$key = $value;
            } catch (e) {
            }
        }

        $data->save();

        return response()->json(["message" => "Data patched successfully"]);
    }

    public function deleteData(Request $request, $id)
    {
        $token = $request->header("Authorization");
        if (!Helpers::verifyToken($token)) {
            return response()->json(["error" => "Invalid token"], 401);
        }
        try {
            $data = $this->model::find($id);
            if (empty($data)) {
                return response()->json(["error" => "No data found."], 404);
            }
            $data->delete();
            return response()->json($data);
        } catch (Exception $e) {
            Log::error("Error deleting data: " . $e->getMessage());
            return response()->json(["error" => "An error occurred while deleting data."], 500);
        }
    }

    public function fetchData(Request $request, $id = null)
    {
        $token = $request->header("Authorization");
        if (!Helpers::verifyToken($token)) {
            return response()->json(["error" => "Invalid token"], 401);
        }

        $result = json_decode($request->getContent(), true);
        $where = $result["where"] ?? null;
        $orWhere = $result["orWhere"] ?? null;

        $data = null;

        try {
            // Fetch the model data
            if ($where) {
                if ($orWhere) {
                    $data = $this->model->where($where)->orWhere($orWhere)->get();
                } else {
                    $data = $this->model->where($where)->get();
                }
            } else {
                if ($id !== -1) {
                    $data = $this->model::find($id);
                } else {
                    $data = $this->model->all();
                }
            }

            if (empty($data)) {
                return response()->json(["error" => "No data found/for this resource."], 404);
            }

            return response()->json($data);
        } catch (Exception $e) {
            Log::error("Error fetching data: " . $e->getMessage());
            return response()->json(["error" => "An error occurred while fetching data."], 500);
        }
    }
}
