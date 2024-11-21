# install
```sh
pip install kivy
``` 

# build
```sh
pip install buildozer

buildozer init
```

Edit buildozer.spec to include permissions for file access:
```
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
```

```sh
buildozer -v android debug
```

