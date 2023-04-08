from django.db import models
from django.template.defaultfilters import slugify as django_slugify
from django.utils.text import slugify
from django.db import IntegrityError, router, transaction
from django.conf import settings

# Slugify (Cyrillic)
alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}

def unidecode(s):
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))

class ModelMixin():

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """автоматическое формирование слага из наименования"""
        if self._state.adding and not self.slug:
            self.slug = self.slugify(self.name)
            using = kwargs.get("using") or router.db_for_write(
                type(self), instance=self
            )
            kwargs["using"] = using
            try:
                with transaction.atomic(using=using):
                    res = super().save(*args, **kwargs)
                return res
            except IntegrityError:
                pass
            # попытка найти существующий слаг со схожим именем
            slugs = set(
                type(self)._default_manager.filter(slug__startswith=self.slug)
                .values_list("slug", flat=True)
            )
            i = 1
            while True:
                slug = self.slugify(self.name, i)
                if slug not in slugs:
                    self.slug = slug
                    return super().save(*args, **kwargs)
                i += 1
        else:
            return super().save(*args, **kwargs)

    def slugify(self, category, i=None):
        if getattr(settings, "TAGGIT_STRIP_UNICODE_WHEN_SLUGIFYING", False):
            slug = slugify(unidecode(category))
        else:
            slug = slugify(category, allow_unicode=True)
        if i is not None:
            slug += "_%d" % i
        return slug

def item_tree(a):
    """создание дерева элементов"""
    def tree(c):
        """запись коментов в поле для детей у родительского элемента"""
        for f in c:
            if f.get("children"):                               # если коментарии имеет детей
                for item in f.get("children"):                  # проход по списку детей
                    for j in a:                                 # проход по списку а
                        if j.get("id") == item:                 # если находим id то у списка детей заменяем элемент на словарь
                            m = f.get("children")
                            ind = m.index(item)
                            m.insert(ind, j)
                            m.remove(item)
                            a.remove(j)
                            f.update(children=m)                # сохраняем элемент в списке детей
                            break
                d = f.get("children")
                m = tree(d)
                f.update(children=m)
        return c

    def add_url(c, url=None):
        """добавление url ключей в словарь"""
        for kkk in c:
            if url:
                kkk["url"] = url + '/' + kkk.get('slug')
            else:
                kkk["url"] = kkk.get('slug')
            if kkk.get('children', None):
                kkk = add_url(kkk.get('children'), kkk.get('url'))
        return c

    cc = []
    for b in a:  # создание нового списка словарей с ключами где хранятся дети
        if b.get("parent_id") != None:
            for r in a:
                if r.get("id") == b.get("parent_id"):
                    if r.get("children") == None:
                        r["children"] = []
                    tttt = r.get('children')
                    tttt.append(b.get("id"))
                    r["children"] = tttt
    v = len(a)
    i = 0
    j = 0
    while i < v:  # удаление из нового списка с коментов без детей
        if not a[j].get("parent_id"):
            cc.append(a.pop(j))
        else:
            j += 1
        i += 1
    c = tree(cc)

    c = add_url(c)

    return c