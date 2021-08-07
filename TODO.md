# Gibooru TODO

Making sure that we *gib* access to all the boorus!

## Todo

- [ ] Add APIs for rule34, Safebooru, furry, konachan, yande.re, sankaku, lolibooru, etc.
- [ ] Add sync (as opposed to async default) support?
- [ ] **Danbooru**: Implement GET notes page API
- [ ] **Gelbooru**: Determine why comment and deleted image API is not responding
- [ ] Add actual error checking perhaps lmao
- [ ] Generalize APIs after they are robust (possibly using ABCs)
- [ ] Test API key effects

## In Progress

- [ ] **Danbooru**: get comments
- [ ] Add pythonic properties


## Done ✓

- ~~[ ] Add QUIC support (nginx only implementing by end of 2021)~~
- [x] Add HTTP/2 support (not even much faster)
- [x] Add more thorough testing
- [x] **Gelbooru**: Implement GET tags page API
- [x] **Gelbooru**: Implement GET posts page API
- [x] **Danbooru**: Implement **kwargs for uncaptured parameters
- [x] **Danbooru**: Implement GET counts page API
- [x] **Danbooru**: Implement GET artists page API
- [x] **Danbooru**: Implement GET explore page API
- [x] **Danbooru**: Implement GET tags page API
- [x] **Danbooru**: Implement GET posts page API