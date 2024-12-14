<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;

class UserController
{
    protected $apiController = null;

    public function __construct()
    {
        $apiController = new APIController();
        $this->apiController = $apiController;
        $this->apiController->setModel(User::class);
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
