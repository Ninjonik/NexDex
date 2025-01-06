<?php

namespace App\Http\Controllers;

use App\Models\Battle;
use App\Models\DroppedCountryball;
use Illuminate\Http\Request;

class DroppedCountryballController
{
    protected $apiController = null;

    public function __construct()
    {
        $apiController = new APIController();
        $this->apiController = $apiController;
        $this->apiController->setModel(DroppedCountryball::class);
    }

    public function postData(Request $request)
    {
        return $this->apiController->postData($request);
    }

    public function patchData(Request $request)
    {
        $token = $request->header("Authorization");
        if (!Helpers::verifyToken($token)) {
            return response()->json(["error" => "Invalid token"], 401);
        }

        $id = intval($request->route('id'));

        $data = DroppedCountryball::find($id);

        if (empty($data)) {
            return response()->json(["error" => "No data found for this resource."], 404);
        }

        $result = json_decode($request->getContent(), true);
        
        if (!empty($data->owner_id) && !array_key_exists("override", $result)) {
            return response()->json(["error" => "This countryball already has an owner."], 404);
        }

        return $this->apiController->patchData($request);
    }

    public function deleteData(Request $request)
    {
        return $this->apiController->deleteData($request, intval($request->route('id')));
    }

    public function getData(Request $request)
    {
        return $this->apiController->fetchData($request, intval($request->route('id') ?? -1));
    }

    public function getDatas(Request $request)
    {
        $token = $request->header("Authorization");
        if (!Helpers::verifyToken($token)) {
            return response()->json(["error" => "Invalid token"], 401);
        }
        $id = intval($request->route('id') ?? -1);

        $model = new DroppedCountryball();

        $result = json_decode($request->getContent(), true);
        $list = $result["list"] ?? [];

        $data = null;

        try {
            $battleModel = [];
            if ($id !== -1) {
                $battleModel = Battle::find($id);
                $attackerCountryballs = json_decode($battleModel->attacker_countryballs, true);
                $defenderCountryballs = json_decode($battleModel->defender_countryballs, true);

                $list = array_unique(array_map('intval', array_merge($attackerCountryballs, $defenderCountryballs)));
            }
            if ($list && count($list) > 0) {
                $data = $model::findMany($list)->keyBy('id');
            } else {
                $data = $model->all()->keyBy('id');
            }

            if (empty($data)) {
                return response()->json(["error" => "No data found/for this resource."], 404);
            }

            return response()->json(["countryballs" => $data, "battle" => $battleModel]);
        } catch (Exception $e) {
            Log::error("Error fetching data: " . $e->getMessage());
            return response()->json(["error" => "An error occurred while fetching data."], 500);
        }
    }
}
