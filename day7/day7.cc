#include <fstream>
#include <ranges>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>
#include <iostream>

class File
{
private:
  unsigned size_;

public:
  File(unsigned s): size_(s) {}

  unsigned getSize() const
  {
    return size_;
  }
};

class Dir
{
private:
  std::unordered_map<std::string, int> subdirs_;
  std::vector<File> files_;

public:
  int parent;

  Dir(int p): parent(p) {}

  void addFile(unsigned size)
  {
    files_.emplace_back(size);
  }
  void addDir(std::string name, int dir)
  {
    std::cout << "Adding dir '" << name << "'" << std::endl;
    subdirs_.emplace(name, dir);
  }
  // Throws if does not exist
  int getDir(const std::string &name)
  {
    std::cout << "Getting dir '" << name << "'" << std::endl;
    return subdirs_.at(name);
  }

  unsigned getSize(const std::vector<Dir> &dirs) const
  {
    unsigned sum = 0;
    for (const File &file : files_)
      sum += file.getSize();
    for (const auto &item : subdirs_)
      sum += dirs[item.second].getSize(dirs);
    return sum;
  }

  void print(std::ostream &os, const std::vector<Dir> &dirs, std::string indent) const
  {
    for (const File &file : files_)
      os << indent << "- (file, size=" << file.getSize() << ")\n";
    for (const auto &item : subdirs_)
    {
      const std::string &name = item.first;
      const Dir &subdir = dirs[item.second];
      os << indent << "- " << name << " (dir, size=" << subdir.getSize(dirs) << ")\n";
      subdir.print(os, dirs, indent + "  ");
    }
  }
};

int main(int argc, char **argv)
{
  if (argc < 2)
    return 1;

  std::vector<Dir> dirs;
  dirs.emplace_back(-1);
  int root = 0;
  dirs[root].parent = root;
  int cwd = root;

  std::ifstream input(argv[1]);
  std::string line;
  while(std::getline(input, line))
  {
    std::cout << ":: " << line << std::endl;
    // Commands
    if (line.starts_with("$ cd "))
    {
      std::string cd = line.substr(5);
      if (cd == "/")
        cwd = root;
      else if (cd == "..")
        cwd = dirs[cwd].parent;
      else
        cwd = dirs[cwd].getDir(cd);
    }
    else if (line == "$ ls")
      continue; // List case, handled anyway
    // List
    else if (line.starts_with("dir "))
    {
      int newdir = dirs.size();
      dirs.emplace_back(cwd);
      dirs[cwd].addDir(line.substr(4), newdir);
    }
    else
    {
      int split_at = line.find(' ');
      unsigned long size = std::stoul(line.substr(0, split_at));
      dirs[cwd].addFile(size);
    }
  }

  std::cout << "- / (dir, size=" << dirs[root].getSize(dirs) << ")\n";
  dirs[root].print(std::cout, dirs, "  ");

  unsigned sum = 0;
  for (unsigned size :
      dirs
      | std::views::transform([&dirs](const Dir &d) { return d.getSize(dirs); })
      | std::views::filter([](unsigned u) { return u <= 100000; }))
    sum += size;

  std::cout << sum << std::endl;
}
