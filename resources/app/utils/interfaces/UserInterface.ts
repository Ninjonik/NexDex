export default interface UserInterface {
  id: number;
  name: string;
  email: string;
  email_verified_at?: Date | null;
  discord_id: string;
  discord_token: string;
  discord_guilds: string;
  created_at: Date;
  updated_at: Date;
}
