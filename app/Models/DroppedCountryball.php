<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class DroppedCountryball extends Model
{

    protected $primaryKey = 'id';

    public function owner(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function countryball(): BelongsTo
    {
        return $this->belongsTo(Countryball::class);
    }
}
