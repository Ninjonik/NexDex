<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Countryball extends Model
{
    use HasFactory;

    public function ability(): BelongsTo
    {
        return $this->belongsTo(Ability::class);
    }

    public function economy(): BelongsTo
    {
        return $this->belongsTo(Economy::class);
    }

    public function faction(): BelongsTo
    {
        return $this->belongsTo(Faction::class);
    }

    public function ideology(): BelongsTo
    {
        return $this->belongsTo(Ideology::class);
    }

    public function regime(): BelongsTo
    {
        return $this->belongsTo(Regime::class);
    }

    public function dropped(): HasMany
    {
        return $this->hasMany(DroppedCountryball::class);
    }
}
