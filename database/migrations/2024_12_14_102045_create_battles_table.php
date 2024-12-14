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
        Schema::create('battles', function (Blueprint $table) {
            $table->string('id')->primary();
            $table->string('name')->nullable();
            $table->text("description")->nullable();
            $table->string('attacker_id');
            $table->string('defender_id');
            $table->json('attacker_countryballs')->default("[]");
            $table->json('defender_countryballs')->default("[]");
            /*
            0 - Waiting for players
            1 - Attacker locked in
            2 - Defender locked in
            3 - Battle end
            4 - Canceled (Attacker)
            5 - Declined (Defender)
            */
            $table->integer('status')->default(0);
            $table->string('winner')->nullable();
            $table->string('channel_id')->nullable();
            $table->dateTime('battle_end')->nullable();
            $table->timestamps();
            $table->foreign('attacker_id')->references('id')->on('users');
            $table->foreign('defender_id')->references('id')->on('users');
            $table->foreign('winner')->references('id')->on('users');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('battles');
    }
};
