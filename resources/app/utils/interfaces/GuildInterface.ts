export default interface GuildInterface {
  id: string;
  name: string;
  icon?: string;
  banner?: string;
  owner: boolean;
  permissions: number;
  permissions_new: string;
  features?: string[];
}