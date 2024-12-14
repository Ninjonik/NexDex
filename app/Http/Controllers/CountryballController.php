<?php

namespace App\Http\Controllers;

use App\Models\Countryball;
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
        return $this->apiController->fetchData($request, intval($request->route('id') ?? -1));
    }
}
