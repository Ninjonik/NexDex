<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('countryballs', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->text("description");
            $table->string("logo");
            $table->string("thumbnail");
            $table->bigInteger('ability_id')->unsigned();
            $table->bigInteger('economy_id')->unsigned();
            $table->bigInteger('faction_id')->unsigned();
            $table->bigInteger('ideology_id')->unsigned();
            $table->bigInteger('regime_id')->unsigned();
            $table->timestamps();
            $table->foreign('ability_id')->references('id')->on('abilities');
            $table->foreign('economy_id')->references('id')->on('economies');
            $table->foreign('faction_id')->references('id')->on('factions');
            $table->foreign('ideology_id')->references('id')->on('ideologies');
            $table->foreign('regime_id')->references('id')->on('regimes');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('countryballs');
    }
};
