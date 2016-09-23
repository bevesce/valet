![icon](icon.png)

# Valet

Valet is an automation system for OSX that runs predefined rules when content of given directory changes.

## Defining rules

To create rule you need to subclass `valet.Rule` and implement two methods:

1. `when` should return True if rule should be applied
2. `then` should define actions that rule executes

```
import valet

class Movies(valet.Rule):
    def when(self):
        return self.is_movie()

    def then(self):
        self.move('~/Movies')

valet.run('~/Downloads')
```

At the end of the file that defines rule for given directory you should run valet pointing to that directory.

### Whens

Available checks to use in `when` method:

- `name_contains(word)`
- `name_contains_all(*args)`
- `name_contains_any(*args)`
- `extension_in(*args)`
- `is_movie()`
- `is_book()`
- `is_image()`
- `is_comic()`
- `is_dir()`
- `has_tag(tag)`

### Thens

Available actions to use in `then` method:

- `move(to_path)`
- `tag(tag)`
- `open()`
- `add_ctimestamp()`
- `trash()`
- `notify(msg, title='Valet')`
- `rename(new_name)`

## Installing rules

Just run `python <path_to_rule> load`.
