<?php

namespace App\Http\Controllers;

use App\Models\User;
use App\Services\JWTService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Http;

class DiscordOAuthController extends Controller
{
    private string $clientId;
    private string $clientSecret;
    private string $redirectUri;
    private string $tokenUrl = 'https://discord.com/api/oauth2/token';
    private string $apiBaseUrl = 'https://discord.com/api/users/@me';
    private string $apiGuildsUrl = 'https://discord.com/api/users/@me/guilds';
    private string $authUrl = 'https://discord.com/api/oauth2/authorize';

    public function __construct()
    {
        $this->clientId = config('services.discord.client_id');
        $this->clientSecret = config('services.discord.client_secret');
        $this->redirectUri = config('services.discord.redirect_uri');
    }

    // Step 1: Redirect to Discord's OAuth page
    public function redirectToDiscord()
    {
        $params = [
            'client_id' => $this->clientId,
            'redirect_uri' => $this->redirectUri,
            'response_type' => 'code',
            'scope' => 'identify email guilds'
        ];

        $discordAuthUrl = $this->authUrl . '?' . http_build_query($params);

        return redirect($discordAuthUrl);
    }

    // Step 2: Handle the callback from Discord
    public function handleCallback(Request $request)
    {
        $code = $request->input('code');

        // Exchange the authorization code for an access token
        $response = Http::asForm()->post($this->tokenUrl, [
            'client_id' => $this->clientId,
            'client_secret' => $this->clientSecret,
            'grant_type' => 'authorization_code',
            'code' => $code,
            'redirect_uri' => $this->redirectUri,
        ]);

        $data = $response->json();

        if (isset($data['access_token'])) {
            $accessToken = $data['access_token'];

            // Get user details from Discord
            $userResponse = Http::withHeaders([
                'Authorization' => 'Bearer ' . $accessToken,
            ])->get($this->apiBaseUrl);

            $discordUser = $userResponse->json();


            $guildsResponse = Http::withHeaders([
                'Authorization' => 'Bearer ' . $accessToken,
            ])->get($this->apiGuildsUrl);

            $discordGuilds = $guildsResponse->json();

            // Filter guilds where the user is owner
            $filteredGuilds = array_filter($discordGuilds, function ($guild) {
                return $guild['owner'] ?? false;
            });

            // Transform filtered guilds into an object with guild IDs as keys
            $guildsObject = json_encode(array_reduce(
                $filteredGuilds,
                function ($carry, $item) {
                    $carry[$item['id']] = $item;
                    return $carry;
                },
                []
            ));

            // Step 3: Check if user exists, if so log them in, else create a new user
            $user = User::where('id', $discordUser['id'])->first();

            if ($user) {
                // Update the user's OAuth token
                $user->update([
                    'discord_token' => $accessToken,
                    'discord_guilds' => $guildsObject,
                    'email' => $discordUser['email'],
                    'name' => $discordUser['username'],
                ]);

                Auth::login($user);
            } else {
                // Create a new user if it doesn't exist yet
                $user = User::create([
                    'id' => $discordUser['id'],
                    'name' => $discordUser['username'],
                    'email' => $discordUser['email'],
                    'discord_token' => $accessToken,
                    'discord_guilds' => $guildsObject,
                ]);

                Auth::login($user);
            }

            // Redirect the user to the intended page
            $token = JWTService::generate();
            $cookie = cookie('token', $token, 60 * 24, null, null, null, false);
            return redirect()->intended('/dashboard')->cookie($cookie);
        }

        // Handle errors (e.g., invalid token or missing code)
        return redirect('/login')->withErrors(['error' => 'Failed to authenticate with Discord.']);
    }

    // Verify the user's token, if valid return the user data from the database based off the "sub" field in JWT
    public function getUserData(Request $request)
    {
        return JWTService::getUserData($request);
    }
}
