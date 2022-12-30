#include <algorithm>
#include <array>
#include <charconv>
#include <cmath>
#include <iostream>
#include <queue>
#include <fstream>
#include <vector>

#define ORE 0
#define CLAY 1
#define OBSIDIAN 2
#define GEODE 3
#define TYPES 4

typedef unsigned short T;
typedef std::array<T, TYPES> Tarray;

struct Resource: Tarray
{
  Resource()
    : Tarray{ 0, 0, 0, 0 }
  {}
  Resource(T ore, T clay, T obsidian, T geode)
    : Tarray{ ore, clay, obsidian, geode }
  {}

  Resource operator+(const Resource rhs) const
  {
    Resource res(
      this->at(ORE) + rhs[ORE], 
      this->at(CLAY) + rhs[CLAY],
      this->at(OBSIDIAN) + rhs[OBSIDIAN],
      this->at(GEODE) + rhs[GEODE]
    );
    return res;
  }
  Resource operator-(const Resource rhs) const
  {
    Resource res(
      this->at(ORE) - rhs[ORE], 
      this->at(CLAY) - rhs[CLAY],
      this->at(OBSIDIAN) - rhs[OBSIDIAN],
      this->at(GEODE) - rhs[GEODE]
    );
    return res;
  }
};

Resource operator*(T scale, const Resource& rhs)
{
  Resource res(
    rhs[ORE] * scale,
    rhs[CLAY] * scale,
    rhs[OBSIDIAN] * scale,
    rhs[GEODE] * scale
  );
  return res;
}

struct Blueprint 
{
  int id;
  std::array<Resource, TYPES> botcosts;
  
  Blueprint(
      int id,
      Resource orebotcost,
      Resource claybotcost,
      Resource obsidianbotcost,
      Resource geodebotcost)
    : id(id),
      botcosts{ orebotcost, claybotcost, obsidianbotcost, geodebotcost }
  {}
};

struct State
{
  Resource inventory;
  Resource bots;
  int remainingtime;

  State(Resource inventory, Resource bots, int remainingtime)
    : inventory(inventory), bots(bots), remainingtime(remainingtime)
  {}
};

int computemaxgeode(const Blueprint &blueprint, int time_limit)
{
  std::queue<State> todo;
  todo.emplace(
      Resource(),
      Resource(1, 0, 0, 0),
      time_limit);
  int maxgeode = -1;

  // We can't build more than 1 bot per minute => we don't need more ore per
  // minute than the maximum we might ever spend on one bot
  Resource maxbotsneeded;
  for (int bottype = 0; bottype < TYPES; ++bottype)
  {
    for (int resourcetype = 0; resourcetype < GEODE; ++resourcetype)
    {
      if (maxbotsneeded[resourcetype] < blueprint.botcosts[bottype][resourcetype])
        maxbotsneeded[resourcetype] = blueprint.botcosts[bottype][resourcetype];
    }
  }
  // we need as many geode bots as possible though
  maxbotsneeded[GEODE] = time_limit;

  while (!todo.empty())
  {
    State &state = todo.front();

    // what if we waited in this state until time was up?
    {
      Resource projection = state.inventory + state.remainingtime * state.bots;
      if (maxgeode < (int)projection[GEODE])
        maxgeode = projection[GEODE];
    }

    // for each resource type
    for (int bottype = 0; bottype < TYPES; ++bottype)
    {
      if (maxbotsneeded[bottype] <= state.bots[bottype])
        continue;

      const Resource &botcost = blueprint.botcosts[bottype];

      // what if we waited in this state until we could build a bot of this type,
      // then built it?
      std::array<int, TYPES> waittimes = { 0 };
      for (int resourcetype = 0; resourcetype < TYPES; ++resourcetype)
      {
        if (botcost[resourcetype] <= state.inventory[resourcetype])
          waittimes[resourcetype] = 0;
        else
        {
          if (state.bots[resourcetype] == 0)
            // we cannot produce this resource
            waittimes[resourcetype] = time_limit; // will abort later
          else 
          {
            int neededresource = botcost[resourcetype] - state.inventory[resourcetype];
            waittimes[resourcetype] =
              std::lround(
                std::ceil(
                  (float)neededresource / (float)state.bots[resourcetype]));
          }
        }
      }
      int maxwaittime = *std::max_element(waittimes.cbegin(), waittimes.cend());

      int timeexpense = maxwaittime + 1;
      if (state.remainingtime < timeexpense)
        continue;
      int remainingtime = state.remainingtime - timeexpense;

      Resource bots = state.bots;
      bots[bottype] += 1;

      Resource projection = state.inventory
        + timeexpense * state.bots
        - botcost;

      // how many geodes could we possibly achieve from that new state?
      // current geode inventory + current geode bot projection + assume we
      // built new geode bots every remaining minute
      T projectedgeodes = projection[GEODE]
        + bots[GEODE] * remainingtime
        + remainingtime * (remainingtime - 1) / 2;
      if (projectedgeodes < maxgeode)
        // do not even propagate this state
        continue;

      todo.emplace(
          projection,
          bots,
          remainingtime);
    }

    todo.pop();
  }

  return maxgeode;
}

int main(int argc, char **argv)
{
  if (argc < 2)
    return 1;

  std::vector<Blueprint> blueprints;
  std::ifstream input(argv[1]);
  std::string line;
  while (std::getline(input, line))
  {
    std::string_view sv(line);
#define REMOVE_PREFIX(prefix) \
    sv.remove_prefix(sizeof(prefix) - 1); // omit \0
#define READ_INT(var)                                                    \
    int var;                                                             \
    {                                                                    \
      auto res = std::from_chars(sv.data(), sv.data() + sv.size(), var); \
      sv.remove_prefix(res.ptr - sv.data());                             \
    }
    REMOVE_PREFIX("Blueprint ");
    READ_INT(id);
    REMOVE_PREFIX(": Each ore robot costs ");
    READ_INT(orebotorecost);
    REMOVE_PREFIX(" ore. Each clay robot costs ");
    READ_INT(claybotorecost);
    REMOVE_PREFIX(" ore. Each obsidian robot costs ");
    READ_INT(obsidianbotorecost);
    REMOVE_PREFIX(" ore and ");
    READ_INT(obsidianbotclaycost);
    REMOVE_PREFIX(" clay. Each geode robot costs ");
    READ_INT(geodebotorecost);
    REMOVE_PREFIX(" ore and ");
    READ_INT(geodebotobsidiancost);

    blueprints.emplace_back(
        id,
        Resource(orebotorecost, 0, 0, 0),
        Resource(claybotorecost, 0, 0, 0),
        Resource(obsidianbotorecost, obsidianbotclaycost, 0, 0),
        Resource(geodebotorecost, 0, geodebotobsidiancost, 0));
  }
  
  // part 1
  int qualities = 0;
  for (const Blueprint &blueprint : blueprints)
    qualities += blueprint.id * computemaxgeode(blueprint, 24);

  std::cout << qualities << std::endl;

  // part 2
  long long largests = 1;
  for (unsigned i = 0; i < 3 && i < blueprints.size(); ++i)
    largests *= computemaxgeode(blueprints[i], 32);

  std::cout << largests << std::endl;
}
