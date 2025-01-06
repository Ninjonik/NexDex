<?php

namespace App\Http\Controllers;

use App\Models\Battle;
use App\Models\Countryball;
use App\Models\DroppedCountryball;
use Illuminate\Http\Request;

class CountryballController
{
    protected $apiController = null;

    public function __construct()
    {
        $apiController = new APIController();
        $this->apiController = $apiController;
        $this->apiController->setModel(Countryball::class);
    }

    public function postData(Request $request)
    {
        return $this->apiController->postData($request);
    }

    public function patchData(Request $request)
    {
        return $this->apiController->patchData($request);
    }

    public function deleteData(Request $request)
    {
        return $this->apiController->deleteData($request, intval($request->route('id')));
    }

    public function getData(Request $request)
    {
        if (!empty($request->route('id')) && $request->route('id') === "drop") {
            return $this->dropACountryBall($request);
        }
        return $this->apiController->fetchData($request, intval($request->route('id') ?? -1));
    }

    public function dropACountryBall(Request $request)
    {
        $token = $request->header("Authorization");
        if (!Helpers::verifyToken($token)) {
            return response()->json(["error" => "Invalid token"], 401);
        }

        $messageId = $request->route('messageId');

        try {
            $data = Countryball::inRandomOrder()->first();

            if (empty($data)) {
                return response()->json(["error" => "No data found/for this resource."], 404);
            }

            $newDrop = new DroppedCountryball();

            $attackModifier = number_format(rand(-50, 50) / 100, 4);  // Get a random 4 digit float number between -0,5 and +0,5
            $hp_modifier = number_format(rand(-50, 50) / 100, 4);  // Get a random 4 digit float number between -0,5 and +0,5

            $newDrop->id = $messageId;
            $newDrop->attack_modifier = $attackModifier;
            $newDrop->hp_modifier = $hp_modifier;
            $newDrop->countryball_id = $data->id;

            $newDrop->save();

            return response()->json(["id" => $messageId, "attack_modifier" => $attackModifier, "hp_modifier" => $hp_modifier, "countryball_id" => $data->id, "countryball" => $data]);
        } catch (Exception $e) {
            Log::error("Error fetching data: " . $e->getMessage());
            return response()->json(["error" => "An error occurred while fetching data."], 500);
        }
    }

    public function getDatas(Request $request)
    {
        $token = $request->header("Authorization");
        if (!Helpers::verifyToken($token)) {
            return response()->json(["error" => "Invalid token"], 401);
        }
        $id = intval($request->route('id') ?? -1);

        $model = new Countryball();

        $result = json_decode($request->getContent(), true);
        $list = $result["list"] ?? [];

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
