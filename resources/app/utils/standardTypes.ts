export const tablePresets = {
  abilities: {
    pluralName: "Abilities",
    singleName: "Ability",
    description: "",
    tabs: [
      {
        label: "All",
        value: "all",
      },
      {
        label: "Active",
        value: "active",
      },
      {
        label: "Inactive",
        value: "inactive",
      },
    ],
  },
  countryballs: {
    pluralName: "Countryballs",
    singleName: "Countryball",
    description: "",
    tabs: [],
  },
  economies: {
    pluralName: "Economies",
    singleName: "Economy",
    description: "",
    tabs: [],
  },
  factions: {
    pluralName: "Factions",
    singleName: "Faction",
    description: "",
    tabs: [],
  },
  ideologies: {
    pluralName: "Ideologies",
    singleName: "Ideology",
    description: "",
    tabs: [],
  },
  regimes: {
    pluralName: "Regimes",
    singleName: "Regime",
    description: "",
    tabs: [],
  },
};

export interface ComponentProps {
  type: keyof typeof tablePresets;
}
