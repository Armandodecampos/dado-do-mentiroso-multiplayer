-- 1. Adiciona a coluna 'name' na tabela 'profiles'
ALTER TABLE public.profiles
ADD COLUMN name VARCHAR(15);

-- 2. Adiciona uma restrição UNIQUE para a coluna 'name'
ALTER TABLE public.profiles
ADD CONSTRAINT profiles_name_key UNIQUE (name);

-- 3. Atualiza a função para extrair o nome do usuário dos metadados no cadastro
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER SET search_path = public
AS $$
BEGIN
  INSERT INTO public.profiles (id, name)
  VALUES (new.id, new.raw_user_meta_data->>'name');
  RETURN new;
END;
$$;
