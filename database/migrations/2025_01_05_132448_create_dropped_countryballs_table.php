<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('dropped_countryballs', function (Blueprint $table) {
            $table->string('id')->primary();
            $table->float("attack_modifier")->default(0);
            $table->float("hp_modifier")->default(0);
            $table->string('owner_id')->nullable();
            $table->bigInteger('countryball_id')->unsigned();
            $table->timestamps();
            $table->foreign('owner_id')->references('id')->on('users');
            $table->foreign('countryball_id')->references('id')->on('countryballs');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('dropped_country_balls');
    }
};
